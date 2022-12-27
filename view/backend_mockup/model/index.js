let posts = [
  {
    id: 0,
    text: "Please note that Twitter will do lots of dumb things in coming months.",
    sentiment: "negative"
  },
  {
    id: 1,
    text: "Russia leaves Kherson. Absolute Ukrainian triumph.",
    sentiment: "positive"
  },
  {
    id: 2,
    text: "It turns out women enjoy having human rights, and we vote.",
    sentiment: "neutral"
  },
  {
    id: 3,
    text: "Alhamdulilah for this victory🤲 Sydney you were amazing. But we are not done yet. 100% focus for Melbourne. Congratulations Pakistanio. 1 to go.",
    sentiment: "positive"
  },
  {
    id: 4,
    text: "Lamar Jackson meeting a young fan with a heart condition will make your day. This is fantastic.",
    sentiment: "positive"
  },
];

let next_id = 5;

exports.create = async (text, sentiment) => {
  let post = {
    id: next_id,
    text: text,
    sentiment: sentiment
  };
  next_id += 1;
  posts.push(post);
  return {
    rows: [post],
  };
}

exports.get = async () => {
  return { rows: posts };
}

exports.remove = async (id) => {
    let original_length = posts.length;
    posts = posts.filter(post => post.id !== id);
    if (posts.length === original_length) {
        throw new Error;
    }
}