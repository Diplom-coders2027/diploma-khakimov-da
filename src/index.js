const express = require('express')
const app = express()
const PORT = 5000

app.set('view engine', 'ejs')
app.use(express.urlencoded({extended: false}))
app.use(express.static('public'))

app.get('/', (req,res) => {
    res.render('index')
})

app.get('/calculator', (req,res) => {
    res.render('calculator')
})

app.get('/weapons', (req,res) => {
    res.render('weapons')
})

app.get('/gadgets', (req,res) => {
    res.render('gadgets')
})

app.get('/specializations', (req,res) => {
    res.render('specializations')
})



app.listen(PORT, () => {
    console.log(`Server started: http://localhost:${PORT}`)
})