const cwGithub = 'https://cwpeng.github.io/test/assignment-3-1';
const google = 'https://www.google.com/';
const myWebsite = 'http://localhost:8000/api/hello';

async function fetchURL(url) {
    try {
        let response = await fetch(url);
        console.log('success', response);
 
        const result = await response.json();
        console.log('body:', result);

    } catch (error) {
        console.error('error', error);
    }
}

fetchURL(cwGithub);
fetchURL(google);
fetchURL(myWebsite);

