export async function createPost(post) {

  const data = new FormData();
  data.append('post', post);
  data.append('username', "user1");
  data.append('title', "title");

  try {
    const res = await fetch('/post/create', {
      method: 'POST',
      body: data,
    });
    return res;
  } catch (err) {
    return err;
  }
}
  
export async function getPosts() {
  try {
    let res = await fetch(`/posts`);
    res = await res.text();
    res = JSON.parse(res);
    return res;
  } catch (err) {
    return err;
  }
}
  
export async function removePost(id) {
  try {
    const res = await fetch(`/post/${id}`, {
      method: 'DELETE',
    });
    return res;
  } catch (err) {
    return err;
  }
}