const http = require("http");

const server = http.createServer((req, res) => {
  const method = req.method;
  const urlParts = req.url.split("?")[0];
  const segments = urlParts.split("/").filter(Boolean);

  // @endpoint GET /vehicles
  if (method === "GET" && segments.length === 1 && segments[0] === "vehicles") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify([
      {
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159864
      },
      {
        "id": 2,
        "nickName": "Dolly",
        "vin": "JN8AZ2KR1AT169594",
        "make": "Nissan",
        "model": "Cube",
        "year": "2010",
        "miles": 59000
      }
    ]));
    return;
  }

  // @endpoint GET /vehicles/:id
  if (method === "GET" && segments.length === 2 && segments[0] === "vehicles") {
    const id = parseInt(segments[1], 10);
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      "id": id,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": 159864
    }));
    return;
  }

  // @endpoint POST /vehicles
  if (method === "POST" && segments.length === 1 && segments[0] === "vehicles") {
    res.writeHead(201, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      "id": 1,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": "159,864"
    }));
    return;
  }

  // @endpoint PATCH /vehicles/:id
  if (method === "PATCH" && segments.length === 2 && segments[0] === "vehicles") {
    const id = parseInt(segments[1], 10);
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      "id": id,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": 159999
    }));
    return;
  }

  // @endpoint DELETE /vehicles/:id
  if (method === "DELETE" && segments.length === 2 && segments[0] === "vehicles") {
    res.writeHead(204, {});
    res.end("");
    return;
  }

  // 404 fallback
  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ "error": "Not Found" }));
});

server.listen(process.env.PORT || 4500);
