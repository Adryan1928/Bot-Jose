const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const URL = 'http://localhost:8000/create_message/';

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('ready', () => {
    console.log('Cliente conectado!');
});

client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

client.on('message_create', message => {
    formated_message = {
        message: message.body,
        number: message.from.replace('@c.us', ''),
    }

    if (formated_message.number == "558498013908"){
        axios.post(URL, formated_message)
            .then(response => {
                console.log('Mensagem enviada para a API:', response.data);
                response.data.message = response.data.message || response.data.detail.message;
                client.sendMessage(message.from, response.data.message ?? response.data.detail.message);
            })
            .catch(error => {
                console.error('Erro ao enviar mensagem para a API:', error);
            });
    }
    console.log(formated_message);
});


client.initialize();
