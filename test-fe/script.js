const video = document.getElementById('video');
const chaptersList = document.getElementById('chapters-list');
const timelineMarkers = document.getElementById('timeline-markers');
const videoUpload = document.getElementById('video-upload');
const uploadButton = document.getElementById('upload-button');

// // Fetch metadata from the backend
// fetch('/api/get-metadata') // Adjust API endpoint as necessary
//     .then(response => response.json())
//     .then(metadata => {
//         const chapters = metadata.chapters;

//         // Add chapters to the side list
//         chapters.forEach((chapter, index) => {
//             const li = document.createElement('li');
//             li.textContent = chapter.title;
//             li.addEventListener('click', () => {
//                 video.currentTime = chapter.start; // Jump to chapter start
//             });
//             chaptersList.appendChild(li);

//             // Add markers to the video timeline
//             const marker = document.createElement('div');
//             const duration = video.duration || 0; // Duration might not be available initially
//             marker.style.left = `${(chapter.start / duration) * 100}%`;
//             marker.style.width = `${((chapter.end - chapter.start) / duration) * 100}%`;
//             marker.classList.add('chapter-marker');
//             timelineMarkers.appendChild(marker);
//         });

//         // Adjust markers once video metadata is loaded
//         video.addEventListener('loadedmetadata', () => {
//             const duration = video.duration;
//             timelineMarkers.innerHTML = ''; // Clear existing markers
//             chapters.forEach(chapter => {
//                 const marker = document.createElement('div');
//                 marker.style.left = `${(chapter.start / duration) * 100}%`;
//                 marker.style.width = `${((chapter.end - chapter.start) / duration) * 100}%`;
//                 marker.classList.add('chapter-marker');
//                 timelineMarkers.appendChild(marker);
//             });
//         });
//     })
//     .catch(err => {
//         console.error('Error fetching metadata:', err);
//         const chapters = [
//             { "start": 0, "end": 30, "title": "Intro" },
//             { "start": 30, "end": 100, "title": "Main Content" },
//             { "start": 100, "end": 127, "title": "Outro" }
//         ];

//         // Add chapters to the side list
//         chapters.forEach((chapter, index) => {
//             const li = document.createElement('li');
//             li.textContent = chapter.title;
//             li.addEventListener('click', () => {
//                 video.currentTime = chapter.start; // Jump to chapter start
//             });
//             chaptersList.appendChild(li);

//             // Add markers to the video timeline
//             const marker = document.createElement('div');
//             const duration = video.duration || 0; // Duration might not be available initially
//             marker.style.width = `${((chapter.end - chapter.start) / duration) * 100}%`;
//             marker.classList.add('chapter-marker');
//             timelineMarkers.appendChild(marker);
//         });

//         // Adjust markers once video metadata is loaded
//         video.addEventListener('loadedmetadata', () => {
//             const duration = video.duration;
//             timelineMarkers.innerHTML = ''; // Clear existing markers
//             chapters.forEach(chapter => {
//                 const marker = document.createElement('div');
//                 marker.style.left = `${(chapter.start / duration) * 100}%`;
//                 marker.style.width = `${((chapter.end - chapter.start) / duration) * 100}%`;
//                 marker.classList.add('chapter-marker');
//                 timelineMarkers.appendChild(marker);
//             });
//         });
//     });

// Handle video upload
uploadButton.addEventListener('click', () => {
    const file = videoUpload.files[0];
    if (file) {
        // Show loader
        document.getElementById('loader').style.display = 'block';
        
        const formData = new FormData();
        formData.append('file', file);

        // Update the video source to the uploaded file
        const videoURL = URL.createObjectURL(file);
        video.src = videoURL;
        video.load(); // Load the new video source

        fetch('http://localhost:8000/api/media-analyzer/vid-to-text', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // Hide loader
                document.getElementById('loader').style.display = 'none';
                console.log('Video uploaded successfully:', data);

                const chapters = data.chapters.chapters;

                // Add chapters to the side list
                chapters.forEach((chapter, index) => {
                    const li = document.createElement('li');
                    li.textContent = chapter.title;
                    li.addEventListener('click', () => {
                        video.currentTime = timeToSeconds(chapter.startTime); // Jump to chapter start
                    });
                    chaptersList.appendChild(li);

                    // Add markers to the video timeline
                    const marker = document.createElement('div');
                    const duration = video.duration || 0;
                    marker.style.width = `${((timeToSeconds(chapter.endTime) - timeToSeconds(chapter.startTime)) / duration) * 100}%`;
                    marker.classList.add('chapter-marker');
                    timelineMarkers.appendChild(marker);
                });

                // Adjust markers once video metadata is loaded
                video.addEventListener('loadedmetadata', () => {
                    const duration = video.duration;
                    timelineMarkers.innerHTML = ''; // Clear existing markers
                    chapters.forEach(chapter => {
                        const marker = document.createElement('div');
                        marker.style.left = `${(timeToSeconds(chapter.startTime) / duration) * 100}%`;
                        marker.style.width = `${((timeToSeconds(chapter.endTime) - timeToSeconds(chapter.startTime)) / duration) * 100}%`;
                        marker.classList.add('chapter-marker');
                        timelineMarkers.appendChild(marker);
                    });
                });
            })
            .catch(error => {
                // Hide loader
                document.getElementById('loader').style.display = 'none';
                console.error('Error uploading video:', error);
            });
    } else {
        alert('Please select a video file to upload.');
    }
}); 


function timeToSeconds(timeString) {
    const [hours, minutes, seconds] = timeString.split(':').map(Number);
    return (hours * 3600) + (minutes * 60) + seconds;
}