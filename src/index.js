const express = require('express')
const path = require('path')
const fs = require('fs/promises')
const app = express()
const PORT = 5000

app.set('view engine', 'ejs')
app.use(express.urlencoded({extended: false}))
app.use(express.static('public'))

app.get('/', (req,res) => {
    res.render('index')
})

const DATA_DIR = path.join(__dirname, 'data');

async function loadJson(fileName) {
  const raw = await fs.readFile(path.join(DATA_DIR, fileName), 'utf-8');
  return JSON.parse(raw);
}

app.get('/weapons', async (req, res, next) => {
  try {
    const [heavy, light, medium] = await Promise.all([
      loadJson('heavy.json'),
      loadJson('light.json'),
      loadJson('medium.json'),
    ]);

    res.render('weapons', {heavy, light, medium});
  } catch (err) {
    next(err);
  }
});

app.get('/about', (req,res) => {
    res.render('about-us')
})

app.listen(PORT, () => {
    console.log(`Server started: http://localhost:${PORT}`)
})