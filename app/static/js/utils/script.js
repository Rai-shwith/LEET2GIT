const scrollCard = (next = true) => {
    const container = document.getElementById('cardContainer');
    const cardWidth = container.querySelector('.flex-none').offsetWidth;
    if (next) {
        container.scrollBy({ left: cardWidth, behavior: 'smooth' });
    } else {
        container.scrollBy({ left: -cardWidth, behavior: 'smooth' });
    }
}