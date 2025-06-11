document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality for cycle tracker
    const cycleTabButtons = document.querySelectorAll('#cycle-tracker .tab-button');
    cycleTabButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all buttons in this tab container
            const tabContainer = this.closest('.tab-container');
            tabContainer.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Hide all tab contents in this container
            tabContainer.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Show the selected tab content
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Activate the first tab by default if no tab is active
    const cycleTabContainer = document.querySelector('#cycle-tracker .tab-container');
    if (cycleTabContainer) {
        const defaultTab = cycleTabContainer.querySelector('.tab-button:first-child');
        if (defaultTab && !cycleTabContainer.querySelector('.tab-button.active')) {
            defaultTab.click();
        }
    }

    // Rest of your existing code...
    // Scroll to section if URL has hash
    if (window.location.hash) {
        const element = document.querySelector(window.location.hash);
        if (element) {
            setTimeout(() => {
                element.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        }
    }

    // Check if we should scroll to a specific element from server
    const scrollToElement = document.getElementById('{{ scroll_to }}');
    if (scrollToElement) {
        setTimeout(() => {
            scrollToElement.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }

    // Calculate BMI if both height and weight are entered
    const heightInput = document.getElementById('Height');
    const weightInput = document.getElementById('Weight');
    const bmiInput = document.getElementById('BMI');
    
    if (heightInput && weightInput && bmiInput) {
        heightInput.addEventListener('input', calculateBMI);
        weightInput.addEventListener('input', calculateBMI);
    }
});

function calculateBMI() {
    const heightInput = document.getElementById('Height');
    const weightInput = document.getElementById('Weight');
    const bmiInput = document.getElementById('BMI');
    
    if (!heightInput || !weightInput || !bmiInput) return;

    const height = parseFloat(heightInput.value) / 100; // convert cm to m
    const weight = parseFloat(weightInput.value);
    
    if (height && weight) {
        const bmi = (weight / (height * height)).toFixed(1);
        bmiInput.value = bmi;
    }
}