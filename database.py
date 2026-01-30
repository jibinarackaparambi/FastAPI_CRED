import sqlite3
from typing import Any
from schemas import CreateShipments,UpdateShipments

class Shipment:
    def __init__(self):
        self.conn = sqlite3.Connection("shipment.db",check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_chipment_db()

    def create_chipment_db(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS shipment  (
            id INT PRIMARY KEY,
            content TEXT,
            weight REAL,
            status TEXT)
        """)
    
    def create(self, shipment:CreateShipments) -> int:
        self.cur.execute("SELECT MAX(id) from shipment")
        data = self.cur.fetchone()
        print(data)
        id =  data[0] + 1 if data and data[0] is not None  else 1
        self.cur.execute("""
        INSERT INTO shipment 
        VALUES(:id,:content,:weight,:status)
            """, {
                "id": id,
                **shipment.model_dump()

            })
        
        self.conn.commit()
        return id
    
    def get(self, id:int) ->dict[str, Any] | None:
        
        self.cur.execute("""SELECT * FROM shipment WHERE id=?""",(id,))
        shipment =  self.cur.fetchone()
        return {
            "id": shipment[0],
            "content": shipment[1],
            "weight": shipment[2],
            "status": shipment[3]
        } if shipment else None
    
    def put(self, id:int, shipment:UpdateShipments) ->dict[str, Any]| None:
        self.cur.execute("""
            UPDATE shipment 
            SET content=:content,weight=:weight,status=:status
            WHERE id=:id
        """,{"content":shipment.content,"weight":shipment.weight,"status":shipment.status,"id":id})
        self.conn.commit()
        self.cur.execute("""SELECT * FROM shipment WHERE id=?""",(id,))
        shipment =  self.cur.fetchone()
        return {
            "id": shipment[0],
            "content": shipment[1],
            "weight": shipment[2],
            "status": shipment[3]
        } if shipment else None
    def patch(self, id: int, shipment: UpdateShipments) -> dict[str, Any] | None:
        data = shipment.model_dump(exclude_none=True)
        if not data:
            return None
        
        fields = ','.join(f"{k}=:{k}" for k in data.keys())
        params = {**data, "id": id}
        
        self.cur.execute(f"""
            UPDATE shipment 
            SET {fields}
            WHERE id = :id
        """, params)
        self.conn.commit()
        # Assuming you want to return the updated row or affected count
        self.cur.execute("SELECT * FROM shipment WHERE id = :id", {"id": id})
        row = self.cur.fetchone()
        return dict(zip(['id', 'content', 'weight', 'status'], row)) if row else None

    def delete(self, id:int):
        self.cur.execute(f"""DELETE FROM shipment WHERE id={id}""")
        self.conn.commit()
        return id