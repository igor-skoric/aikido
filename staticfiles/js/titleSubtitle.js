document.querySelectorAll('.accordion-toggle').forEach(btn => {

      btn.addEventListener('click', () => {
        const panel = btn.nextElementSibling;
        const icon = btn.querySelector('.icon');
        const isOpen = panel.style.maxHeight && panel.style.maxHeight !== '0px';

        if (isOpen) {
          panel.style.maxHeight = '0px';
          icon.textContent = '+';
        } else {
          // Prvo zatvorimo sve unutar tog nivoa (opciono ako želiš samo jedan otvoren po sekciji)
          const siblings = btn.parentElement.parentElement.querySelectorAll('.accordion-panel');
          siblings.forEach(sib => {
            if (sib !== panel) {
              sib.style.maxHeight = '0px';
              const siblingIcon = sib.previousElementSibling?.querySelector('.icon');
              if (siblingIcon) siblingIcon.textContent = '+';
            }
          });

          // Otvaranje
          panel.style.maxHeight = panel.scrollHeight + 'px';
          icon.textContent = '−';
        }

        // Ako je ugnježden, propagira max-height naviše
        let parent = panel.parentElement;
        while (parent) {
          if (parent.classList.contains('accordion-panel')) {
            parent.style.maxHeight =  '500px';
          }
          parent = parent.parentElement;
        }
      });




    });