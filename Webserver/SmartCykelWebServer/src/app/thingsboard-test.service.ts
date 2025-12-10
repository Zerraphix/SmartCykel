import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThingsboardTestService {

  private tbBaseUrl = 'https://demo.thingsboard.io';
  private jwtToken  = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtZXBqMDRAZ21haWwuY29tIiwidXNlcklkIjoiNzcxY2E1NTAtOTg1YS0xMWYwLWE5YjUtNzkyZTIxOTRhNWQ0Iiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiJhMmUyODY4Yy05YWUyLTQzYzktYWZjMS02ZDRmOGRkNDVmMTUiLCJleHAiOjE3NjY5ODEzMDMsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNzY1MTgxMzAzLCJmaXJzdE5hbWUiOiJNYXRoaWFzIiwibGFzdE5hbWUiOiJKZW5zZW4iLCJlbmFibGVkIjp0cnVlLCJwcml2YWN5UG9saWN5QWNjZXB0ZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiI3NzA2YWM1MC05ODVhLTExZjAtYTliNS03OTJlMjE5NGE1ZDQiLCJjdXN0b21lcklkIjoiMTM4MTQwMDAtMWRkMi0xMWIyLTgwODAtODA4MDgwODA4MDgwIn0.zRLzeKC-C3iO90XAXJ7wnIXKC84Ntwws164na4xx0IByxKzhJohtaQ2OpsygRF48bbisNy_LLwpvRq6NYKCXeg';          // JWT from /api/auth/login (NOT device token)
  private deviceId  = '37767a50-985c-11f0-a9b5-792e2194a5d4';

  constructor(private http: HttpClient) {}

  /** Test REST call: get latest telemetry using JWT */
  getLatestTelemetry(): Observable<any> {
  const keys = [
    'battery_charging',
    'battery_current',
    'battery_remaining_hours',
    'battery_remaining_mah',
    'battery_remaining_text',
    'battery_soc',
    'battery_state',
    'battery_voltage',
    'humidity',
    'latitude',
    'longitude',
  ].join(',');

  const url = `${this.tbBaseUrl}/api/plugins/telemetry/DEVICE/${this.deviceId}/values/timeseries?keys=${keys}&limit=1`;

  const headers = new HttpHeaders({
    'X-Authorization': `Bearer ${this.jwtToken}`
  });

  return this.http.get(url, { headers });
}

// Dette virker ikke
  sendTestTelemetryWithDeviceToken(deviceToken: string): Observable<any> {
    const url = `${this.tbBaseUrl}/api/v1/${deviceToken}/telemetry`;

    const body = {
      temperature: 25,
      humidity: 50
    };

    return this.http.post(url, body);
  }
}
