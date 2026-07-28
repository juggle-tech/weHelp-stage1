// track.js
logTime('track.js downloaded');
// console.log('track.js downloaded, execution started');

const imageUrl = 'https://picsum.photos/4000/3000';

const xhr = new XMLHttpRequest();
xhr.open('GET', imageUrl, false);
xhr.send();

logTime('Get image');

document.getElementById('preview').src = imageUrl;

console.log('Large image finished loading, track.js execution finished');