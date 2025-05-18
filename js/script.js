// Attendre que le DOM soit complètement chargé
document.addEventListener('DOMContentLoaded', function() {
    // Préchargeur
    const preloader = document.querySelector('.preloader');
    
    // Simuler un temps de chargement pour montrer le préchargeur (réduit à 1.5s)
    setTimeout(function() {
        preloader.classList.add('hidden');
        // Activer les animations une fois le préchargeur masqué
        setTimeout(function() {
            initializeAnimations();
        }, 500);
    }, 1500);
    
    // Initialisation des variables
    const cursor = document.querySelector('.cursor');
    const cursorFollower = document.querySelector('.cursor-follower');
    const navbar = document.querySelector('.navbar');
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    const viewDetailsButtons = document.querySelectorAll('.view-details');
    const modalCloseButtons = document.querySelectorAll('.modal-close');
    const contactForm = document.getElementById('contactForm');
    const skillProgressBars = document.querySelectorAll('.skill-progress');
    
    // ===== CURSEUR PERSONNALISÉ =====
    function updateCursor(e) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        // Ajouter un léger délai pour le suiveur du curseur
        setTimeout(function() {
            cursorFollower.style.left = e.clientX + 'px';
            cursorFollower.style.top = e.clientY + 'px';
        }, 80);
    }
    
    document.addEventListener('mousemove', updateCursor);
    
    // Effet d'agrandissement du curseur sur les éléments interactifs
    const interactiveElements = document.querySelectorAll('a, button, input, textarea, .project-card, .skill-item, .social-link, .filter-btn');
    
    interactiveElements.forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            cursor.classList.add('active');
            cursorFollower.classList.add('active');
        });
        
        element.addEventListener('mouseleave', function() {
            cursor.classList.remove('active');
            cursorFollower.classList.remove('active');
        });
    });
    
    // ===== NAVIGATION =====
    // Effet de scroll sur la navbar
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Mettre à jour la classe active sur les liens de navigation
        updateActiveNavLink();
    });
    
    // Menu mobile
    menuToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
    
    // Fermer le menu mobile lors du clic sur un lien
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            menuToggle.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
    
    // Mettre à jour la classe active sur les liens de navigation
    function updateActiveNavLink() {
        const scrollPosition = window.scrollY;
        
        document.querySelectorAll('section').forEach(function(section) {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    // Défilement fluide pour les liens d'ancrage
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            
            // Ne rien faire si c'est un lien vers un modal
            if (targetId.startsWith('#modal-')) return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ===== EFFET MACHINE À ÉCRIRE =====
    function typeEffect() {
        const typedTextElement = document.querySelector('.typed-text');
        const cursorElement = document.querySelector('.cursor-typed');
        const textArray = ["Développeur en formation", "Étudiant en BUT Informatique", "Passionné de programmation", "Créateur de solutions"];
        let textArrayIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;
        
        function type() {
            const currentText = textArray[textArrayIndex];
            
            if (isDeleting) {
                typedTextElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
                typingSpeed = 50;
            } else {
                typedTextElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
                typingSpeed = 100;
            }
            
            if (!isDeleting && charIndex === currentText.length) {
                // Pause à la fin du texte
                isDeleting = true;
                typingSpeed = 1500;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textArrayIndex = (textArrayIndex + 1) % textArray.length;
                typingSpeed = 500;
            }
            
            setTimeout(type, typingSpeed);
        }
        
        if (typedTextElement) {
            setTimeout(type, 1000);
        }
    }
    
    // ===== FILTRAGE DES PROJETS =====
    filterBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            // Retirer la classe active de tous les boutons
            filterBtns.forEach(function(btn) {
                btn.classList.remove('active');
            });
            
            // Ajouter la classe active au bouton cliqué
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            // Filtrer les projets
            projectCards.forEach(function(card) {
                if (filter === 'all' || card.getAttribute('data-category').includes(filter)) {
                    card.style.display = 'block';
                    setTimeout(function() {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(function() {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
    
    // ===== MODALS =====
    // Ouvrir les modals
    viewDetailsButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const projectId = this.getAttribute('data-project');
            const modal = document.getElementById('modal-' + projectId);
            
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });
    
    // Fermer les modals
    modalCloseButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        });
    });
    
    // Fermer les modals en cliquant en dehors du contenu
    document.querySelectorAll('.modal').forEach(function(modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    });
    
    // ===== ANIMATIONS AU DÉFILEMENT =====
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8 &&
            rect.bottom >= 0
        );
    }
    
    function animateOnScroll() {
        // Animation des barres de compétences
        skillProgressBars.forEach(function(bar) {
            if (isElementInViewport(bar) && !bar.classList.contains('animated')) {
                const level = bar.getAttribute('data-level');
                bar.style.width = level + '%';
                bar.classList.add('animated');
            }
        });
        
        // Animation des sections
        document.querySelectorAll('.section-header, .about-content, .skills-category, .project-card, .timeline-item, .experience-card, .contact-container').forEach(function(element) {
            if (isElementInViewport(element) && !element.classList.contains('animated')) {
                element.classList.add('animated');
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    }
    
    // ===== ANIMATION DES PARTICULES =====
    function animateParticles() {
        const particles = document.querySelectorAll('.particle');
        
        particles.forEach(function(particle, index) {
            // Position aléatoire
            const randomX = Math.random() * 100;
            const randomY = Math.random() * 100;
            
            particle.style.left = randomX + '%';
            particle.style.top = randomY + '%';
            
            // Taille aléatoire
            const randomSize = Math.random() * 10 + 5;
            particle.style.width = randomSize + 'px';
            particle.style.height = randomSize + 'px';
            
            // Opacité aléatoire
            const randomOpacity = Math.random() * 0.3 + 0.1;
            particle.style.opacity = randomOpacity;
            
            // Animation aléatoire
            const randomDuration = Math.random() * 20 + 10;
            particle.style.animationDuration = randomDuration + 's';
            particle.style.animationDelay = (index * 0.2) + 's';
        });
    }
    
    // ===== VALIDATION DU FORMULAIRE =====
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simuler l'envoi du formulaire
            const submitBtn = this.querySelector('.submit-btn');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<span>Envoi en cours...</span> <i class="fas fa-spinner fa-spin"></i>';
            submitBtn.disabled = true;
            
            // Simuler un délai d'envoi
            setTimeout(function() {
                // Réinitialiser le formulaire
                contactForm.reset();
                
                // Afficher un message de succès
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.innerHTML = '<i class="fas fa-check-circle"></i> Votre message a été envoyé avec succès!';
                successMessage.style.color = '#00b894';
                successMessage.style.padding = '1.5rem';
                successMessage.style.marginBottom = '2rem';
                successMessage.style.backgroundColor = 'rgba(0, 184, 148, 0.1)';
                successMessage.style.borderRadius = '5px';
                successMessage.style.display = 'flex';
                successMessage.style.alignItems = 'center';
                successMessage.style.gap = '1rem';
                
                contactForm.insertBefore(successMessage, contactForm.firstChild);
                
                // Restaurer le bouton
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Supprimer le message après 5 secondes
                setTimeout(function() {
                    successMessage.style.opacity = '0';
                    setTimeout(function() {
                        successMessage.remove();
                    }, 300);
                }, 5000);
            }, 2000);
        });
    }
    
    // ===== EFFET PARALLAXE =====
    function parallaxEffect() {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.pageYOffset;
            
            // Parallaxe sur la section héro
            const heroContent = document.querySelector('.hero-content');
            if (heroContent) {
                heroContent.style.transform = 'translateY(' + scrollPosition * 0.2 + 'px)';
            }
            
            // Parallaxe sur les particules
            const particles = document.querySelectorAll('.particle');
            particles.forEach(function(particle, index) {
                const speed = 0.05 + (index * 0.01);
                particle.style.transform = 'translateY(' + scrollPosition * speed + 'px)';
            });
        });
    }
    
    // ===== INITIALISATION DES ANIMATIONS =====
    function initializeAnimations() {
        // Initialiser les éléments pour l'animation au défilement
        document.querySelectorAll('.section-header, .about-content, .skills-category, .project-card, .timeline-item, .experience-card, .contact-container').forEach(function(element) {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            element.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        });
        
        // Animer les éléments visibles au chargement
        animateOnScroll();
        
        // Animer les particules
        animateParticles();
        
        // Initialiser l'effet de machine à écrire
        typeEffect();
        
        // Initialiser l'effet parallaxe
        parallaxEffect();
        
        // Déclencher l'animation au défilement
        window.addEventListener('scroll', animateOnScroll);
    }
    
    // ===== INITIALISATION DU PORTFOLIO =====
    // Mettre à jour la classe active sur les liens de navigation au chargement
    updateActiveNavLink();
    
    // Initialiser le filtrage des projets (afficher tous par défaut)
    document.querySelector('.filter-btn[data-filter="all"]').classList.add('active');
});

// ===== CHARGEMENT DE LA PAGE =====
window.addEventListener('load', function() {
    // Animation d'entrée pour le héros
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        heroContent.style.opacity = '1';
        heroContent.style.transform = 'translateY(0)';
    }
});
