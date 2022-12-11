const express = require('express');
const { create, read, remove } = require('../controller');

const router = express.Router();

router.get("/posts", read);
router.post('/post/create', create);
router.delete('/post/:id', remove);

module.exports = router;