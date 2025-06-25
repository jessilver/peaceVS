document.addEventListener('DOMContentLoaded', function() {
    console.log('Frontend web carregado!');
});

document.addEventListener('DOMContentLoaded', function() {
    /**
     * Função que inicializa UM carrossel individual.
     * @param {HTMLElement} carouselElement - O elemento principal do carrossel a ser inicializado.
     */
    function initCarousel(carouselElement) {
        // --- ETAPA 1: Encontrar todos os elementos DENTRO do carrossel atual ---
        const carouselInnerWrapper = carouselElement.querySelector('.carousel-inner-wrapper');
        const cardWrapper = carouselElement.querySelector('.card-wrapper');
        const prevButton = carouselElement.querySelector('.carousel-control-prev');
        const nextButton = carouselElement.querySelector('.carousel-control-next');
        
        // Se algum elemento essencial não for encontrado, não continua.
        if (!cardWrapper || !prevButton || !nextButton) {
            console.error("Estrutura do carrossel incompleta em:", carouselElement);
            return;
        }

        // --- LÓGICA DO HOVER PARA RESOLVER O RECORTE ---
        if (carouselInnerWrapper) {
            carouselElement.addEventListener('mouseenter', () => {
                carouselInnerWrapper.classList.add('is-hovering');
            });
            carouselElement.addEventListener('mouseleave', () => {
                carouselInnerWrapper.classList.remove('is-hovering');
            });
        }
        
        const originalCardsHTML = cardWrapper.innerHTML;
        let isTransitioning = false;
        let currentIndex = 0;

        function getItemsVisible() {
            if (window.innerWidth < 768) return 2; // Media query do CSS é 576px, mas 768px pode ser mais seguro
            if (window.innerWidth < 992) return 3;
            return 6;
        }

        function getCardWidth() {
            const firstCard = cardWrapper.querySelector('.carousel-card');
            if (!firstCard) return 0;
            return firstCard.getBoundingClientRect().width;
        }

        function setupCarousel() {
            cardWrapper.innerHTML = originalCardsHTML;
            const cards = cardWrapper.querySelectorAll('.carousel-card');
            const cardCount = cards.length;
            const itemsVisible = getItemsVisible();

            // Lógica de clonagem
            for (let i = 0; i < itemsVisible; i++) {
                if (cards[i]) {
                    const clone = cards[i].cloneNode(true);
                    clone.classList.add('clone');
                    cardWrapper.appendChild(clone);
                }
            }
            for (let i = cardCount - 1; i >= cardCount - itemsVisible; i--) {
                if (cards[i]) {
                    const clone = cards[i].cloneNode(true);
                    clone.classList.add('clone');
                    cardWrapper.insertBefore(clone, cardWrapper.firstChild);
                }
            }
            
            currentIndex = itemsVisible;
            reposition(false);
        }

        function reposition(animated = true) {
            const cardWidth = getCardWidth();
            if (!animated) cardWrapper.classList.add('no-transition');
            cardWrapper.style.transform = `translateX(${-currentIndex * cardWidth}px)`;
            if (!animated) {
                cardWrapper.offsetHeight; 
                cardWrapper.classList.remove('no-transition');
            }
        }

        function moveCarousel(direction) {
            if (isTransitioning) return;
            isTransitioning = true;
            currentIndex += direction;
            reposition(true);
        }

        cardWrapper.addEventListener('transitionend', () => {
            const itemsVisible = getItemsVisible();
            const allClonedCards = cardWrapper.querySelectorAll('.clone');
            const originalCardCount = cardWrapper.querySelectorAll('.carousel-card').length - allClonedCards.length;
            
            if (currentIndex >= originalCardCount + itemsVisible) {
                currentIndex = itemsVisible;
                reposition(false);
            }
            if (currentIndex < itemsVisible) {
                currentIndex = originalCardCount + itemsVisible -1;
                reposition(false);
            }
            isTransitioning = false;
        });

        nextButton.addEventListener('click', () => moveCarousel(1));
        prevButton.addEventListener('click', () => moveCarousel(-1));

        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                setupCarousel();
            }, 250);
        });

        setupCarousel();
    } // --- FIM DA FUNÇÃO initCarousel ---


    // --- ETAPA 2: Encontrar TODOS os carrossels e inicializar cada um ---
    const allCarousels = document.querySelectorAll('.carousel.slide');
    allCarousels.forEach(carousel => {
        initCarousel(carousel);
    });

});