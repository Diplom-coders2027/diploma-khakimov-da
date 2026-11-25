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


const cache = new Map();
async function loadJson(name) {
  if (!cache.has(name)) {
    const raw = await fs.readFile(path.join(__dirname, 'data', `${name}.json`), 'utf8');
    cache.set(name, JSON.parse(raw));
  }
  return cache.get(name);
}


async function loadMany(names) {
  const values = await Promise.all(names.map(loadJson));
  return Object.fromEntries(names.map((n, i) => [n, values[i]]));
}


const page = (view, files) => async (req, res, next) => {
  try {
    res.render(view, await loadMany(files));
  } catch (err) {
    next(err);
  }
};


app.get('/weapons', page('weapons', ['heavy', 'light', 'medium']));
app.get('/specializations',   page('specializations',   ['heavy', 'light', 'medium']));
app.get('/gadgets', page('gadgets', ['heavy', 'light', 'medium']));



app.get('/about', (req,res) => {
    res.render('about-us')
})

app.listen(PORT, () => {
    console.log(`Server started: http://localhost:${PORT}`)
})