import { LitElement, html, css } from 'lit-element';
import 'pay-trail-e2';

export class LitElementExample extends LitElement {
  static get properties() {
    return {
      products: { type: Array },
      paytrailField: { type: Object },
    };
  }

  static get styles() {
    return css`
      .product-container {
        display: flex;
        flex-direction: column;
      }
    `;
  }

  constructor() {
    super();
    this.products = [];
  }

  firstUpdated() {
    this.paytrailField = this.shadowRoot.querySelector('pay-trail');
  }

  addProduct() {
    const newProd = {
      item_id: this.products.length,
      item_title: `Product name ${this.products.length}`,
      item_unit_price: '29.99',
      item_vat_percent: '24.00',
    };
    this.products = [...this.products, newProd];
    this.paytrailField.addProducts(newProd);
    this.paytrailField.calculateAuthCodeString();
  }

  removeProduct() {
    const poppedProduct = this.products.pop();
    this.requestUpdate();
    this.paytrailField.removeProduct(poppedProduct);
    this.paytrailField.calculateAuthCodeString();
  }

  render() {
    return html`
      <pay-trail
        MERCHANT_ID="13466"
        URL_SUCCESS="http://www.example.com/success"
        URL_CANCEL="http://www.example.com/cancel"
        PARAMS_IN="MERCHANT_ID,URL_SUCCESS,URL_CANCEL,ORDER_NUMBER,PARAMS_IN,PARAMS_OUT,PAYER_PERSON_PHONE,PAYER_PERSON_EMAIL,PAYER_PERSON_FIRSTNAME,PAYER_PERSON_LASTNAME,PAYER_COMPANY_NAME,PAYER_PERSON_ADDR_STREET,PAYER_PERSON_ADDR_POSTAL_CODE,PAYER_PERSON_ADDR_TOWN,PAYER_PERSON_ADDR_COUNTRY,AMOUNT"
        PARAMS_OUT="ORDER_NUMBER,PAYMENT_ID,AMOUNT,CURRENCY,PAYMENT_METHOD,TIMESTAMP,STATUS"
        PAYER_PERSON_PHONE="01234567890"
        PAYER_PERSON_EMAIL="john.doe@example.com"
        PAYER_PERSON_FIRSTNAME="John"
        PAYER_PERSON_LASTNAME="Doe"
        PAYER_COMPANY_NAME="Test Company"
        PAYER_PERSON_ADDR_STREET="Test Street 1"
        PAYER_PERSON_ADDR_POSTAL_CODE="608009"
        PAYER_PERSON_ADDR_TOWN="Test Town"
        PAYER_PERSON_ADDR_COUNTRY="AA"
        submit_button_label="Pay here"
      ></pay-trail>

      <button @click=${this.addProduct}>Add Product</button>
      <button @click=${this.removeProduct}>Remove Product</button>

      <div class="product-container">
        ${this.products.map(prod => html`<p>${prod.item_title}</p>`)}
      </div>
    `;
  }
}
