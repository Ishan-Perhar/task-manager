from app.database.database import engine

try:
    connection = engine.connect()
    print("DB connected to Succefully")
    connection.close()

except Exception as e:
    print("Connection Failed")
    print(e)

