import React from 'react';

const RecommendedVideos = () => {
    const filters = ["All", "From PlayStation", "Trailers", "Related", "Live", "Gaming", "Computers"];

    const videos = [
        {
            id: 1,
            title: "Resident Evil Requiem - 4th Trailer | PS5 Games",
            channel: "PlayStation",
            views: "841k views",
            time: "5 days ago",
            duration: "2:20",
            thumbnail: "https://placehold.co/320x180/000000/FFFFFF.png?text=Resident+Evil+Requiem",
            verified: true
        },
        {
            id: 2,
            title: "Grand Theft Auto VI Trailer 2",
            channel: "Rockstar Games",
            views: "150m views",
            time: "9 months ago",
            duration: "2:47",
            thumbnail: "https://placehold.co/320x180/000000/FFFFFF.png?text=GTA+VI",
            verified: true
        },
        {
            id: 3,
            title: "SEYON | Kamal Haasan | Sivakarthikeyan",
            channel: "Raaj Kamal Films International",
            views: "15m views",
            time: "1 day ago",
            duration: "3:31",
            thumbnail: "https://placehold.co/320x180/000000/FFFFFF.png?text=SEYON",
            verified: true
        },
        {
            id: 4,
            title: "Bloody Valentine - Glimpse | DC | Lokesh Kanagaraj",
            channel: "Sun TV",
            views: "2.1m views",
            time: "4 days ago",
            duration: "1:38",
            thumbnail: "https://placehold.co/320x180/000000/FFFFFF.png?text=Bloody+Valentine",
            verified: true
        },
        {
            id: 5,
            title: "God of War Ragnarök - Valhalla DLC Trailer",
            channel: "PlayStation",
            views: "12m views",
            time: "1 month ago",
            duration: "12:10",
            thumbnail: "https://placehold.co/320x180/000000/FFFFFF.png?text=God+of+War",
            verified: true
        },
        {
            id: 6,
            title: "Elden Ring: Shadow of the Erdtree Gameplay",
            channel: "Bandai Namco",
            views: "8.5m views",
            time: "2 weeks ago",
            duration: "15:45",
            thumbnail: "https://placehold.co/320x180/000000/FFFFFF.png?text=Elden+Ring",
            verified: true
        },
        {
            id: 7,
            title: "Black Myth: Wukong - Final Trailer",
            channel: "Game Science",
            views: "4.2m views",
            time: "3 days ago",
            duration: "4:12",
            thumbnail: "https://placehold.co/320x180/000000/FFFFFF.png?text=Black+Myth+Wukong",
            verified: true
        }
    ];

    return (
        <div className="recommended-section">
            {/* Filter Chips */}
            <div className="filter-chips">
                {filters.map((filter, index) => (
                    <button
                        key={index}
                        className={`chip ${index === 0 ? 'active' : ''}`}
                    >
                        {filter}
                    </button>
                ))}
                <button className="chip-next-btn">{'>'}</button>
            </div>

            {/* Video List */}
            <div className="video-list">
                {videos.map((video) => (
                    <div key={video.id} className="video-card-horizontal">
                        <div className="thumbnail-wrapper">
                            <img src={video.thumbnail} alt={video.title} />
                            <span className="duration-badge">{video.duration}</span>
                        </div>
                        <div className="video-info-small">
                            <h3 title={video.title}>{video.title}</h3>
                            <div className="channel-name">
                                {video.channel}
                                {video.verified && <span className="verified-badge">✓</span>}
                            </div>
                            <div className="meta-text">
                                {video.views} • {video.time}
                            </div>
                        </div>
                        <button className="more-options-btn">⋮</button>
                    </div>
                ))}
            </div>

            {/* Shorts Shelf Placeholder */}
            <div className="shorts-shelf">
                <div className="shorts-header">
                    <span className="shorts-icon">🩳</span>
                    <h3>Shorts</h3>
                </div>
                <div className="shorts-grid">
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="short-card">
                            <div className="short-thumb" style={{ backgroundImage: `url(https://placehold.co/180x320/222/FFF.png?text=Short+${i})` }}></div>
                            <h4>Peaky Blinders Ed...</h4>
                            <p>1.2M views</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default RecommendedVideos;
