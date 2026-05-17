import sqlite3
import json

class ManualCrawlPipeline:
    def open_spider(self, spider):
        # Connect to SQLite database (creates it if it doesn't exist)
        self.conn = sqlite3.connect('sklearn_data.db')
        self.cur = self.conn.cursor()

        self.cur.execute("PRAGMA foreign_keys = ON;")
        
        # Create table for the main components
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                component_name TEXT,
                examples TEXT
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
        # Insert the main component
        self.cur.execute("""
            INSERT INTO components (url, component_name, examples)
            VALUES (?, ?, ?)
        """, (
            item.get('url', ''),
            item.get('component_name', ''),
            item.get('examples', '')
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
