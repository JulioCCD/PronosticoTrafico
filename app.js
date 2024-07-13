const express = require("express");
const path = require('path');
const mysql = require('mysql');
const app = express();

// Configuración para el motor de plantillas EJS
app.set("view engine", "ejs");

// Middleware para servir archivos estáticos
app.use(express.static(path.join(__dirname, 'public')));

// Configuración de la conexión a la base de datos MySQL
const connection = mysql.createConnection({
    host: '34.151.233.27',  // Cambia a la dirección de tu servidor MySQL si es diferente
    user: 'Pesheto',       // Nombre de usuario de MySQL
    password: 'pesheto69',       // Contraseña de MySQL (deja en blanco si no tienes configurada una contraseña)
    database: 'conteo' // Nombre de tu base de datos
});

// Conectar a la base de datos MySQL
connection.connect(err => {
    if (err) {
        console.error('Error conectando a la base de datos: ', err.stack);
        return;
    }
    console.log('Conectado a la base de datos MySQL');
});

// Ruta principal que muestra datos de la base de datos
app.get("/", (req, res) => {
    // Consulta a la base de datos
    connection.query('SELECT * FROM pronostico', (error, results, fields) => {
        if (error) {
            console.error('Error al realizar la consulta: ', error.stack);
            return res.status(500).send('Error al obtener los datos de la base de datos');
        }
        // Renderizar la vista 'reco' y pasar los resultados de la consulta como datos
        res.render("reco", { conteo: results });
    });
});

app.get("/estadistica", (req, res) => {
    // Consulta a la base de datos
    connection.query('SELECT * FROM pronostico', (error, results, fields) => {
        if (error) {
            console.error('Error al realizar la consulta: ', error.stack);
            return res.status(500).send('Error al obtener los datos de la base de datos');
        }
        // Renderizar la vista 'estadistica' y pasar los resultados de la consulta como datos
        res.render("estadistica", { conteo: results });
    });
});

let datetimeFromDatabase = new Date('2024-07-06T13:30:00'); // Suponiendo que aquí obtienes la fecha y hora desde tu base de datos

// Obtener solo la hora y minutos
let horaMinutos = datetimeFromDatabase.getHours() + ':' + datetimeFromDatabase.getMinutes();

console.log(horaMinutos);

app.get("/about", (req,res)=>{
    res.render("about")
})

app.get("/reco", (req,res)=>{
    res.render("reco")
})

app.get("/estadistica", (req,res)=>{
    res.render("estadistica")
})

// Iniciar el servidor
const PORT = process.env.PORT || 8093;
app.listen(PORT,"0.0.0.0", () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
});

// Manejo de cierre de la conexión cuando se termina la aplicación
process.on('SIGINT', () => {
    connection.end();
    console.log('Conexión a la base de datos cerrada');
    process.exit();
});
