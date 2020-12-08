console.log('script conectado')

const callAPI = async() => {
   const response = await fetch('http://localhost:3000/upload-image')
   const json = await response.json()
   if (json.url !== ""){
   const imageContainer = document.getElementById('image-container')
   imageContainer.src = json.url
   const text = document.getElementById('change-text')
   text.style.display = 'block'
   }
   return json
}

callAPI()