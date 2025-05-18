// Validation améliorée du formulaire de contact
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        const subjectInput = document.getElementById('subject');
        const messageInput = document.getElementById('message');
        
        // Fonction pour valider l'email
        function isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }
        
        // Fonction pour créer et afficher un message d'erreur
        function showError(input, message) {
            // Supprimer l'erreur précédente si elle existe
            const existingError = input.parentElement.querySelector('.error-message');
            if (existingError) {
                existingError.remove();
            }
            
            // Créer et ajouter le message d'erreur
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = message;
            input.parentElement.appendChild(errorDiv);
            input.classList.add('input-error');
        }
        
        // Fonction pour supprimer un message d'erreur
        function removeError(input) {
            const existingError = input.parentElement.querySelector('.error-message');
            if (existingError) {
                existingError.remove();
            }
            input.classList.remove('input-error');
        }
        
        // Validation en temps réel pour le nom
        nameInput.addEventListener('input', function() {
            if (this.value.trim().length < 2) {
                showError(this, 'Le nom doit contenir au moins 2 caractères');
            } else {
                removeError(this);
            }
        });
        
        // Validation en temps réel pour l'email
        emailInput.addEventListener('input', function() {
            if (!isValidEmail(this.value.trim())) {
                showError(this, 'Veuillez entrer une adresse email valide');
            } else {
                removeError(this);
            }
        });
        
        // Validation en temps réel pour le sujet
        subjectInput.addEventListener('input', function() {
            if (this.value.trim().length < 3) {
                showError(this, 'Le sujet doit contenir au moins 3 caractères');
            } else {
                removeError(this);
            }
        });
        
        // Validation en temps réel pour le message
        messageInput.addEventListener('input', function() {
            if (this.value.trim().length < 10) {
                showError(this, 'Le message doit contenir au moins 10 caractères');
            } else {
                removeError(this);
            }
        });
        
        // Validation à la soumission du formulaire
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            let isValid = true;
            
            // Vérifier le nom
            if (nameInput.value.trim().length < 2) {
                showError(nameInput, 'Le nom doit contenir au moins 2 caractères');
                isValid = false;
            }
            
            // Vérifier l'email
            if (!isValidEmail(emailInput.value.trim())) {
                showError(emailInput, 'Veuillez entrer une adresse email valide');
                isValid = false;
            }
            
            // Vérifier le sujet
            if (subjectInput.value.trim().length < 3) {
                showError(subjectInput, 'Le sujet doit contenir au moins 3 caractères');
                isValid = false;
            }
            
            // Vérifier le message
            if (messageInput.value.trim().length < 10) {
                showError(messageInput, 'Le message doit contenir au moins 10 caractères');
                isValid = false;
            }
            
            // Si le formulaire est valide, simuler l'envoi
            if (isValid) {
                const submitBtn = this.querySelector('button[type="submit"]');
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
                }, 1500);
            }
        });
    }
});
