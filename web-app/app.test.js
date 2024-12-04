const request = require('supertest');
const app = require('./app');

let server;

describe('Ping Utility App', () => {
    beforeAll((done) => {
        server = app.listen(4000, () => done());
    });

    afterAll((done) => {
        server.close(done);
    });

    it('should render the homepage', async () => {
        const response = await request(server).get('/');
        expect(response.status).toBe(200);
        expect(response.text).toContain('<h1>Ping Utility</h1>');
    });
});

