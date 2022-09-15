
const nodeHtmlToImage = require('node-html-to-image')
const fs = require('fs');

const image = fs.readFileSync('./face01.jpg');
const base64Image = new Buffer.from(image).toString('base64');
const dataURI = 'data:image/jpeg;base64,' + base64Image

const _htmlTemplate=`<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <style>
      body {
        font-family: "Poppins", Arial, Helvetica, sans-serif;
        background: rgb(00, 00, 00);
        color: #fff;
        width: 900px;
        height: 600px;
      }
      img {
        width: 200px;
        height: 200px;
        position: absolute;
        padding: 10px;
        left: 10px;
        top: 10px;
      }
      .app {
        width: 900px;
        height: 600px;
        padding: 20px;
        display: flex;
        flex-direction: row;
        border-top: 3px solid rgb(180, 00, 00);
        background: rgb(31, 31, 31);
        align-items: center;
      }

      
    </style>
  </head>
  <body>
    <div class="app">
        <img src="{{imageSource}}" />
        <h4>Welcome</h4>
    </div>
  </body>
</html>
`

nodeHtmlToImage({
    output: './image.png',
    html: _htmlTemplate,
    content: { imageSource: dataURI }
  })
    .then(() => console.log('The image was created successfully!'))