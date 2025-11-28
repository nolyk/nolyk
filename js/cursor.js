document.addEventListener('DOMContentLoaded', () => {
   
    const cursor = document.createElement('div');
    cursor.className = 'cursor';
    document.body.appendChild(cursor);
    
    
    createParticles();
    
    
    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;
    const speed = 0.2;
    
    const animateCursor = () => {
        const dx = mouseX - cursorX;
        const dy = mouseY - cursorY;
        cursorX += dx * speed;
        cursorY += dy * speed;
        
        cursor.style.left = `${cursorX}px`;
        cursor.style.top = `${cursorY}px`;
        requestAnimationFrame(animateCursor);
    };
    animateCursor();
    
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    
    const interactiveElements = document.querySelectorAll(
    'a, button, .tech-icons img, .social-icon, .logo, .gradient-text, .skills-btn, .skill-block'
    );
    
    interactiveElements.forEach(el => {
        el.addEventListener('mouseover', () => {
            cursor.classList.add('cursor-hover');
        });
        
        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('cursor-hover');
        });
    });
    
    document.addEventListener('mousedown', () => {
        cursor.classList.add('cursor-active');
    });
    
    document.addEventListener('mouseup', () => {
        cursor.classList.remove('cursor-active');
    });
    

    function createParticles() {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'particles';
        document.body.appendChild(particlesContainer);
        
        const particleCount = 150; 
        
        for (let i = 0; i < particleCount; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.className = `particle type-${Math.floor(Math.random() * 4) + 1}`;
                
              
                const size = Math.random() * 4 + 1; 
                const posX = Math.random() * window.innerWidth;
                const duration = Math.random() * 15 + 10; 
                const delay = Math.random() * 10;
                const drift = (Math.random() - 0.5) * 200; 
                
                particle.style.setProperty('--start-x', `${posX}px`);
                particle.style.setProperty('--drift', `${drift}px`);
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${posX}px`;
                particle.style.animationDuration = `${duration}s`;
                particle.style.animationDelay = `${delay}s`;
                
                
                if (Math.random() > 0.7) {
                    particle.style.animation = `fall ${duration}s linear ${delay}s infinite, twinkle ${Math.random() * 3 + 2}s ease infinite`;
                } else {
                    particle.style.animation = `fall ${duration}s linear ${delay}s infinite`;
                }
                
                particlesContainer.appendChild(particle);
                
               
                setTimeout(() => {
                    particle.remove();
                }, (duration + delay) * 1000);
            }, i * 100); 
        }
        
        setInterval(() => {
            if (particlesContainer.children.length < particleCount/2) {
                const needed = particleCount - particlesContainer.children.length;
                for (let i = 0; i < needed; i++) {
                    createParticle(particlesContainer);
                }
            }
        }, 2000);
        
       
        setInterval(() => {
            particlesContainer.innerHTML = '';
            for (let i = 0; i < particleCount; i++) {
                setTimeout(() => createParticle(particlesContainer), i * 100);
            }
        }, 30000);
    }
    
    function createParticle(container) {
        const particle = document.createElement('div');
        particle.className = `particle type-${Math.floor(Math.random() * 4) + 1}`;
        
        const size = Math.random() * 4 + 1;
        const posX = Math.random() * window.innerWidth;
        const duration = Math.random() * 15 + 10;
        const delay = Math.random() * 10;
        const drift = (Math.random() - 0.5) * 200;
        
        particle.style.setProperty('--start-x', `${posX}px`);
        particle.style.setProperty('--drift', `${drift}px`);
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${posX}px`;
        particle.style.animationDuration = `${duration}s`;
        particle.style.animationDelay = `${delay}s`;
        
        if (Math.random() > 0.7) {
            particle.style.animation = `fall ${duration}s linear ${delay}s infinite, twinkle ${Math.random() * 3 + 2}s ease infinite`;
        } else {
            particle.style.animation = `fall ${duration}s linear ${delay}s infinite`;
        }
        
        container.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, (duration + delay) * 1000);
    }
});