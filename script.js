// I’m Beck.
// Listen for the DOMContentLoaded event to ensure the DOM is fully loaded before executing subsequent code.
document.addEventListener('DOMContentLoaded', () => {
  // Get the add item form and item list elements from the page.
  const addItemForm = document.getElementById('addItemForm');
  const itemList = document.getElementById('itemList');

  // Add a submit event listener to the add item form.
  addItemForm.addEventListener('submit', async (e) => {
      // Prevent the default form submission behavior.
      e.preventDefault();

      // Retrieve the item's name, description, price, and quantity from the form.
      const name = document.getElementById('itemName').value;
      const description = document.getElementById('itemDescription').value;
      const price = document.getElementById('itemPrice').value;
      const quantity = document.getElementById('itemQuantity').value;

      // Use the fetch API to send a POST request to the backend to add a new item.
      await fetch('/api/items', {
          method: 'POST', // The request method is POST.
          headers: { 'Content-Type': 'application/json' }, // Set the request header to indicate that the data sent is in JSON format.
          body: JSON.stringify({ name, description, price, quantity }), // Serialize the form data into JSON format.
      });

      // Reset the form to clear the input fields.
      addItemForm.reset();

      // Reload the item list to update the display on the page.
      loadItems();
  });

  // Define the function to load the item list.
  async function loadItems() {
      // Use the fetch API to send a GET request to the backend to retrieve the item list.
      const response = await fetch('/api/items');
      const items = await response.json(); // Parse the response data as JSON.

      // Clear the HTML content of the item list.
      itemList.innerHTML = '';

      // Iterate over the item list, create a list item for each item, and add it to the item list.
      items.forEach((item) => {
          const li = document.createElement('li'); // Create a new list item element.
          // Set the text content of the list item to display the item's details.
          li.textContent = `ID: ${item.id}, Name: ${item.name}, Description: ${item.description}, Price: $${item.price}, Quantity: ${item.quantity}`;
          itemList.appendChild(li); // Add the list item to the item list.
      });
  }

  // Immediately call the loadItems function after the page is loaded to initialize the item list.
  loadItems();
});