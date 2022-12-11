const express = require('express');
require('dotenv').config();
const routes = require('./routes/index');

// Running express server
const app = express();
const port = process.env.PORT || 8000;

// route middlewares
app.use('/api', routes);

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});