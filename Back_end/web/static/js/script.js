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

        cards = cardWrapper.querySelectorAll('.carousel-card'); 
        if(cards.length <6) {
            console.error("Carrossel deve ter pelo menos 6 cards para funcionar corretamente:", carouselElement);
            prevButton.style.display = 'none';
            nextButton.style.display = 'none';
            cardWrapper.classList.add('no-transition');
            cardWrapper.style.transform = 'translateX(0)';
            carouselInnerWrapper.classList.add('no-transition');
            carouselInnerWrapper.style.width = '100%';
            carouselInnerWrapper.style.overflow = 'hidden';
            carouselElement.classList.add('carousel-no-transition');
            carouselElement.style.width = '100%';
            carouselElement.style.overflow = 'hidden';
            carouselElement.style.position = 'relative';
            carouselElement.style.display = 'flex';
            carouselElement.style.justifyContent = 'center';
            carouselElement.style.alignItems = 'center';    
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

            // Remove clones antigos
            cardWrapper.querySelectorAll('.clone').forEach(clone => clone.remove());

            // Só clona se houver mais de 5 cards
            if (cardCount > 5) {
                // Lógica de clonagem para loop infinito
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
                currentIndex = Math.min(itemsVisible, cardCount);
                reposition(false);
            }
        }

        function reposition(animated = true) {
            const cardWidth = getCardWidth();
            const cards = cardWrapper.querySelectorAll('.carousel-card');
            const cardCount = cards.length;
            const itemsVisible = getItemsVisible();
            // Limita o índice para não sair do range
            if (currentIndex > cardCount + itemsVisible) currentIndex = itemsVisible;
            if (currentIndex < 0) currentIndex = 0;
            if (!animated) cardWrapper.classList.add('no-transition');
            cardWrapper.style.transform = `translateX(${-currentIndex * cardWidth}px)`;
            if (!animated) {
                cardWrapper.offsetHeight;
                cardWrapper.classList.remove('no-transition');
            }
        }

        function moveCarousel(direction) {
            const cards = cardWrapper.querySelectorAll('.carousel-card');
            const cardCount = cards.length;
            const itemsVisible = getItemsVisible();
            if (cardCount <= itemsVisible) return; // Não move se não há o suficiente
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