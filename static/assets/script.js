// Get all the "Remove" buttons
const removeButtons = document.querySelectorAll(
  '[data-tooltip-target^="tooltipRemoveItem"]'
);  

// Add a click event listener to each button
removeButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const slug =
      button.dataset.tooltipTarget.split("tooltipRemoveItem")[1];
    removeCartItem(slug);
  });
});

async function removeCartItem(slug) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const url = `/api/products/${slug}/cart/`;

  const response = await fetch(url, {
          method: 'DELETE',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
          },
          body: {
            "quantity": -1,
          }
      });

    if (response.ok) {
        const itemElement = document.querySelector(`#cartItem${slug}`);
        itemElement.remove();
    }else{
      console.log(response.text);
    }

}
