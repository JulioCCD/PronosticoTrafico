const express=require("express")
const app=express()
const path = require('path');

// Configurar la carpeta 'public' para servir archivos estáticos
app.use(express.static(path.join(__dirname, 'public')));

app.set("view engine","ejs")


app.get("/reco", (req,res)=>{
    res.render("reco")
})

app.get("/about", (req,res)=>{
    res.render("about")
})

app.get("/estadistica", (req,res)=>{
    res.render("estadistica")
})

app.listen(8091, (req,res)=>{
    console.log("Corriendo en el puerto 8091")
}) 