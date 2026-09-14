# main.py
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import FileResponse
import httpx

app = FastAPI(title="Rick and Morty Collector API")

# URL de la API externa
RICK_AND_MORTY_URL = "https://rickandmortyapi.com/api/character"

@app.get("/")
async def read_index():
    # Sirve el archivo index.html que debe estar en la misma carpeta
    return FileResponse("index.html")

@app.get("/personajes/buscar")
async def buscar_personaje_por_nombre(
    nombre: str = Query(..., description="Nombre del personaje a buscar")
):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(RICK_AND_MORTY_URL, params={"name": nombre})
            
            if response.status_code == 404:
                return {"total_encontrados": 0, "personajes": []}
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Error en la API externa")

            data = response.json()
            
            # Formatear la respuesta según el esquema solicitado
            personajes_formateados = []
            for p in data.get("results", []):
                personajes_formateados.append({
                    "id": p["id"],
                    "nombre": p["name"],
                    "estado": p["status"],
                    "especie": p["species"],
                    "imagen": p["image"],
                    "origen": p["origin"]["name"]
                })

            return {
                "total_encontrados": len(personajes_formateados),
                "personajes": personajes_formateados
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)