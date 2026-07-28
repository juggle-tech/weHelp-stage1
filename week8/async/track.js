logTime('track.js downloaded');
// console.log('track.js downloaded, execution started');

const imageUrl = 'https://picsum.photos/3000/2000';

const xhr = new XMLHttpRequest();
xhr.open('GET', imageUrl, false);
xhr.send();

logTime('Get large image');

document.getElementById('largeImg').src = imageUrl;

console.log('Large image finished loading, track.js execution finished');