async function fetchImages(documentName, pageNumber) {
    try {
        const response = await fetch(`/api/getImages?documentName=${encodeURIComponent(documentName)}&pageNumber=${encodeURIComponent(pageNumber)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch images: ${response.statusText}`);
        }

        const images = await response.json();
        displayImages(images);
    } catch (error) {
        console.error('Error fetching images:', error);
    }
}

function displayImages(images) {
    const imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = '';

    images.forEach(image => {
        const imgElement = document.createElement('img');
        imgElement.src = `data:image/png;base64,${image.image_data}`;
        imgElement.alt = 'Context Image';
        imgElement.style.maxWidth = '100%';
        imgElement.style.margin = '10px 0';
        imageContainer.appendChild(imgElement);
    });

