const formidable = require('formidable');
const { create, get, remove } = require('../model/index');

exports.create = (req, res) => {
    const form = new formidable.IncomingForm();
    form.keepExtensions = true;
    form.parse(req, async (err, fields) => {
        if (!fields.text) {
            return res.status(400).json({
                error: 'Text is required',
            });
        }
        const { text, sentiment } = fields;
        try {
            const newPost = await create(text, sentiment);
            return res.status(201).send({ data: newPost.rows[0] });
        } catch (error) {
            return res.status(400).json({
                error,
            });
        }
    });
};

exports.read = async (req, res) => {
    try {
        const posts = await get();
        res.status(200).json(posts);
    } catch (error) {
        res.status(400).json(error);
    }
};

exports.remove = async (req, res) => {
    const id = Number(req.params.id);
    try {
        await remove(id);
        res.sendStatus(200);
    } catch (error) {
        res.status(400).json(error);
    }
}