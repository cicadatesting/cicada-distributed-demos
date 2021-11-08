import http from 'k6/http';
import { sleep } from 'k6';
import { uuidv4 } from "https://jslib.k6.io/k6-utils/1.3.0/index.js";

export default function () {
    const data = {
        name: "jeremy",
        age: 23,
        email: `${uuidv4()}@gmail.com`
    }

    const resp = http.post(
        "http://localhost:8080/users",
        JSON.stringify(data),
        { headers: { 'Content-Type': 'application/json' } }
    );

    console.log("resp:", JSON.stringify(resp, null, 2));
    sleep(1);
}
