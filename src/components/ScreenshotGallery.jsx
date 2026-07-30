import { useEffect, useState } from "react";

function ScreenshotGallery() {

    const [images, setImages] = useState([]);

    useEffect(() => {

        const fetchImages = async () => {

            try {

                const response = await fetch(
                    "http://127.0.0.1:5000/gallery"
                );

                const data = await response.json();

                setImages(data);

            } catch (error) {

                console.log("Gallery not available.");

            }

        };

        fetchImages();

        const interval = setInterval(fetchImages, 1000);

        return () => clearInterval(interval);

    }, []);

    return (
    <div
        style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: "16px",
            padding: "20px"
        }}
    >
        {images.map((image, index) => (

            <img
                key={index}
                src={`http://127.0.0.1:5000/screenshots/${image}`}
                alt="Threat"
                style={{
                    width: "100%",
                    height: "140px",
                    objectFit: "cover",
                    borderRadius: "12px"
                }}
            />

        ))}
    </div>
);

}

export default ScreenshotGallery;
