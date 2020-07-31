import React, { useState } from 'react';
import 'pay-trail-e2';

function App(props) {
    const [products, setProducts] = useState([]);

    function addProduct() {
        const newProd = {
            item_id: products.length,
            item_title: `Product name ${products.length}`,
            item_unit_price: '29.99',
            item_vat_percent: '24.00',
        };
        setProducts([...products, newProd]);

        const paytrail = document.querySelector('pay-trail');
        paytrail.addProducts(newProd);
        paytrail.calculateAuthCodeString();
    }

    function removeProduct() {
        let currentProducts = [...products];
        const poppedProduct = currentProducts.pop();
        setProducts(currentProducts);

        const paytrail = document.querySelector('pay-trail');
        paytrail.removeProduct(poppedProduct);
        paytrail.calculateAuthCodeString();
    }

    function listProducts() {
        return products.map((prod, i) => <p key={i}>{prod.item_title}</p>);
    }

    return (
        <div className="App">
            <pay-trail></pay-trail>
            <button onClick={addProduct}>Add Product</button>
            <button onClick={removeProduct}>Remove Product</button>

            <div className="product-container">{listProducts()}</div>
        </div>
    );
}

export default App;
