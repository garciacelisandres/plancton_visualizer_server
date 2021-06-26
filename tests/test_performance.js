import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  duration: '1m',
  vus: 10,
  thresholds: {
    http_req_duration: ['p(80)<2000'],
  },
};

export default function () {
  const res = http.get('https://plankton.westeurope.cloudapp.azure.com/api/v0.1/samples');
  sleep(1);
}