// Get all the "Remove" buttons
const removeButtons = document.querySelectorAll(
  '[data-tooltip-target^="tooltipRemoveItem"]'
);  

// Add a click event listener to each button
removeButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const itemId =
      button.dataset.tooltipTarget.split("tooltipRemoveItem")[1];
    removeCartItem(itemId);
  });
});

async function removeCartItem(itemId) {
  try {
    // await fetch(`/api/cart/${itemId}`, {
    //   method: "DELETE",
    // });
    const itemElement = document.querySelector(`#cartItem${itemId}`);
    itemElement.remove();
    
  } catch (error) {
    console.error("Error removing item from cart:", error);
    alert("Failed to remove item from cart. Please try again.");
  }
}
