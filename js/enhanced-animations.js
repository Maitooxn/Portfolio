/**
 * Script pour les animations et transitions améliorées
 * Développé par Jordan Oshoffa
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des animations
    initSectionAnimations();
    initParallaxEffect();
    initSkillsAnimation();
    initProjectCardEffects();
    initCustomCursor();
    initSmoothScrolling();
    initMenuToggle();
    initTypingEffect();
    
    // Masquer le préchargeur une fois la page chargée
    setTimeout(function() {
        document.querySelector('.preloader').style.opacity = '0';
        document.querySelector('.preloader').style.visibility = 'hidden';
    }, 1000);
});

/**
 * Animation des sections au défilement
 */
function initSectionAnimations() {
    // Ajouter la classe section-fade-in à toutes les sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.add('section-fade-in');
    });
    
    // Observer les sections pour les animer lors du défilement
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Observer les éléments avec animation retardée
    const delayedElements = document.querySelectorAll('.skill-item, .project-card, .info-item');
    const delayedObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Ajouter un délai progressif pour chaque élément
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, 100 * index);
            }
        });
    }, { threshold: 0.1 });
    
    delayedElements.forEach(element => {
        element.classList.add('section-fade-in');
        delayedObserver.observe(element);
    });
}

/**
 * Effet de parallaxe pour l'arrière-plan
 */
function initParallaxEffect() {
    // Ajouter la classe parallax-bg aux éléments concernés
    const parallaxElements = document.querySelectorAll('.hero, .about, .skills, .projects, .contact');
    parallaxElements.forEach(element => {
        element.classList.add('parallax-bg');
    });
    
    // Effet de parallaxe au défilement
    window.addEventListener('scroll', function() {
        const scrollPosition = window.pageYOffset;
        
        document.querySelectorAll('.parallax-bg').forEach(element => {
            const speed = 0.5;
            const yPos = -(scrollPosition * speed);
            element.style.backgroundPosition = `center ${yPos}px`;
        });
        
        // Effet de parallaxe pour les particules
        document.querySelectorAll('.particle').forEach((particle, index) => {
            const speed = 0.1 + (index % 3) * 0.05;
            const yPos = -(scrollPosition * speed);
            particle.style.transform = `translateY(${yPos}px)`;
        });
    });
}

/**
 * Animation des barres de compétences
 */
function initSkillsAnimation() {
    const skillBars = document.querySelectorAll('.skill-progress');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const level = entry.target.getAttribute('data-level');
                entry.target.style.width = `${level}%`;
            }
        });
    }, { threshold: 0.1 });
    
    skillBars.forEach(bar => {
        observer.observe(bar);
    });
}

/**
 * Effets pour les cartes de projets
 */
function initProjectCardEffects() {
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        // Ajouter un overlay pour l'effet de survol
        const overlay = document.createElement('div');
        overlay.classList.add('project-overlay');
        card.appendChild(overlay);
        
        // Ajouter la classe pour l'animation au survol
        card.classList.add('hover-lift');
    });
}

/**
 * Curseur personnalisé
 */
function initCustomCursor() {
    const cursor = document.querySelector('.cursor');
    const cursorFollower = document.querySelector('.cursor-follower');
    
    if (!cursor || !cursorFollower) return;
    
    document.addEventListener('mousemove', function(e) {
        cursor.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
        
        // Ajouter un léger délai pour le suiveur
        setTimeout(() => {
            cursorFollower.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
        }, 50);
    });
    
    // Effet au survol des éléments cliquables
    const clickables = document.querySelectorAll('a, button, .btn, .project-card, .nav-item, .logo');
    
    clickables.forEach(element => {
        element.addEventListener('mouseenter', function() {
            cursor.classList.add('active');
            cursorFollower.classList.add('active');
        });
        
        element.addEventListener('mouseleave', function() {
            cursor.classList.remove('active');
            cursorFollower.classList.remove('active');
        });
    });
}

/**
 * Défilement fluide pour les ancres
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (!targetElement) return;
            
            // Animation de défilement fluide
            window.scrollTo({
                top: targetElement.offsetTop - 80, // Offset pour la barre de navigation
                behavior: 'smooth'
            });
            
            // Mettre à jour la classe active dans la navigation
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
    
    // Mettre à jour la navigation active au défilement
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        
        document.querySelectorAll('section').forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
}

/**
 * Animation du menu mobile
 */
function initMenuToggle() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (!menuToggle || !navMenu) return;
    
    menuToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        navMenu.classList.toggle('active');
        
        // Animation des éléments du menu
        const navItems = navMenu.querySelectorAll('.nav-item');
        navItems.forEach((item, index) => {
            if (navMenu.classList.contains('active')) {
                // Animation d'entrée
                item.style.transitionDelay = `${0.1 + index * 0.05}s`;
                item.style.transform = 'translateY(0)';
                item.style.opacity = '1';
            } else {
                // Animation de sortie
                item.style.transitionDelay = `${0.05 * (navItems.length - index)}s`;
                item.style.transform = 'translateY(20px)';
                item.style.opacity = '0';
            }
        });
    });
    
    // Fermer le menu au clic sur un lien
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            menuToggle.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
}

/**
 * Effet de texte tapé à la machine
 */
function initTypingEffect() {
    const typedTextElement = document.querySelector('.typed-text');
    if (!typedTextElement) return;
    
    const texts = [
        "Développeur Web",
        "Développeur Java",
        "Développeur Python",
        "Étudiant en Informatique",
        "Passionné de Programmation"
    ];
    
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;
    
    function type() {
        const currentText = texts[textIndex];
        
        if (isDeleting) {
            // Supprimer des caractères
            typedTextElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50;
        } else {
            // Ajouter des caractères
            typedTextElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100;
        }
        
        // Gérer la fin de la frappe ou de la suppression
        if (!isDeleting && charIndex === currentText.length) {
            // Pause à la fin du texte
            isDeleting = true;
            typingSpeed = 1000;
        } else if (isDeleting && charIndex === 0) {
            // Passer au texte suivant
            isDeleting = false;
            textIndex = (textIndex + 1) % texts.length;
            typingSpeed = 500;
        }
        
        setTimeout(type, typingSpeed);
    }
    
    // Démarrer l'effet de frappe
    setTimeout(type, 1000);
}

/**
 * Animation pour les boutons de détail et de jeu
 */
function initDetailPlayButtons() {
    const detailsBtn = document.getElementById('details-btn');
    const playBtn = document.getElementById('play-btn');
    const detailsSection = document.getElementById('details');
    const playSection = document.getElementById('play');
    
    if (!detailsBtn || !playBtn || !detailsSection || !playSection) return;
    
    // Masquer les sections au chargement
    detailsSection.style.display = 'none';
    playSection.style.display = 'none';
    
    detailsBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (detailsSection.style.display === 'none') {
            // Masquer la section de jeu avec animation
            if (playSection.style.display !== 'none') {
                playSection.classList.remove('active');
                setTimeout(() => {
                    playSection.style.display = 'none';
                }, 600);
            }
            
            // Afficher la section de détails avec animation
            detailsSection.style.display = 'block';
            setTimeout(() => {
                detailsSection.classList.add('active');
            }, 10);
            
            detailsBtn.classList.add('active');
            playBtn.classList.remove('active');
            
            // Défilement fluide vers la section
            detailsSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            // Masquer la section de détails avec animation
            detailsSection.classList.remove('active');
            setTimeout(() => {
                detailsSection.style.display = 'none';
            }, 600);
            
            detailsBtn.classList.remove('active');
        }
    });
    
    playBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (playSection.style.display === 'none') {
            // Masquer la section de détails avec animation
            if (detailsSection.style.display !== 'none') {
                detailsSection.classList.remove('active');
                setTimeout(() => {
                    detailsSection.style.display = 'none';
                }, 600);
            }
            
            // Afficher la section de jeu avec animation
            playSection.style.display = 'block';
            setTimeout(() => {
                playSection.classList.add('active');
            }, 10);
            
            playBtn.classList.add('active');
            detailsBtn.classList.remove('active');
            
            // Défilement fluide vers la section
            playSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            // Masquer la section de jeu avec animation
            playSection.classList.remove('active');
            setTimeout(() => {
                playSection.style.display = 'none';
            }, 600);
            
            playBtn.classList.remove('active');
        }
    });
}

// Initialiser les boutons de détail et de jeu pour chaque page de projet
if (document.getElementById('details-btn')) {
    initDetailPlayButtons();
}
