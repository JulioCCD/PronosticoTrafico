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

  <title>Mi Página</title>

  <style>

    body {

      font-family: Arial, sans-serif;

      text-align: center;

      margin-top: 20%;

    }

    h1 {

      color: #4CAF50;

    }

  </style>

</head>

<body>

  <h1>Bienvenidos a mi página</h1>

</body>

</html>

 `);

});



server.listen(port, hostname, () => {

 console.log(`Server running at http://${hostname}:${port}/`);

}); 
