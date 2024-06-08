const http = require('node:http');



const hostname = '0.0.0.0';

const port = 8091;



const server = http.createServer((req, res) => {

 res.statusCode = 200;

 res.setHeader('Content-Type', 'text/html');

 res.end(`

  <!DOCTYPE html>

  <html lang="es">

  <head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Bienvenidos a Radiaciones Solares</title>

    <style>

      body {

        font-family: Arial, sans-serif;

        margin: 0;

        padding: 0;

        background-color: #f2f2f2;

        text-align: center;

      }

      header {

        background-color: #4CAF50;

        color: white;

        padding: 20px;

      }

      .container {

        margin-top: 50px;

      }

      h1 {

        font-size: 36px;

        margin-bottom: 20px;

      }

      p {

        font-size: 18px;

      }

      .btn {

        display: inline-block;

        background-color: #4CAF50;

        color: white;

        padding: 10px 20px;

        text-decoration: none;

        border-radius: 5px;

        transition: background-color 0.3s ease;

      }

      .btn:hover {

        background-color: #45a049;

      }

    </style>

  </head>

  <body>

    <header>

      <h1>PRONOSTICOS DEL TIEMPO</h1>

    </header>

    <div class="container">

      <h1>BienvenidosS AL PRONOSTICO</h1>

      <p>¡Descubre todo sobre las predicciones DEL TIEMPO EN EL 10!</p>

      <a href="#" class="btn">Empezar</a>

    </div>

  </body>

  </html>

 `);

});



server.listen(port, hostname, () => {

 console.log(`Server running at http://${hostname}:${port}/`);

}); 
