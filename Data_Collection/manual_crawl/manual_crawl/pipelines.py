import sqlite3
import json

class ManualCrawlPipeline:
    def open_spider(self, spider):
        # Connect to SQLite database
        self.conn = sqlite3.connect('sklearn_data.db')
        self.cur = self.conn.cursor()

        self.cur.execute("PRAGMA foreign_keys = ON;")
        
        # 1. ADDED structured_body TO THE COMPONENTS TABLE
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                component_name TEXT,
                examples TEXT,
                structured_body TEXT
            )
        """)
        
        # Create table for the parameters
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                component_id INTEGER,
                parameter_name TEXT,
                description TEXT,
                FOREIGN KEY (component_id) REFERENCES components (id)
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # 2. UPDATED SQL INSERT TO EXPECT AND SAVE STRUCURED BODY
        self.cur.execute("""
            INSERT INTO components (url, component_name, examples, structured_body)
            VALUES (?, ?, ?, ?)
        """, (
            item.get('url', ''),
            item.get('component_name', ''),
            item.get('examples', ''),
            item.get('structured_body', '')
        ))
        
        # Get the ID of the inserted component
        component_id = self.cur.lastrowid
        
        # Insert all parameters linked to this component
        parameters = item.get('parameters', [])
        for param in parameters:
            self.cur.execute("""
                INSERT INTO parameters (component_id, parameter_name, description)
                VALUES (?, ?, ?)
            """, (
                component_id,
                param.get('parameter', ''),
                param.get('description', '')
            ))
            
        # Commit the transaction
        self.conn.commit()
        return item