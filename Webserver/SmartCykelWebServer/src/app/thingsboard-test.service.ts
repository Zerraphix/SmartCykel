import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThingsboardTestService {

  private tbBaseUrl = 'https://demo.thingsboard.io';
  private jwtToken  = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtZXBqMDRAZ21haWwuY29tIiwidXNlcklkIjoiNzcxY2E1NTAtOTg1YS0xMWYwLWE5YjUtNzkyZTIxOTRhNWQ0Iiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiI3YjJjNmQ4ZC02YjA3LTQzZjYtOGM1Yi0yNGEyNmNkMmRkMTIiLCJleHAiOjE3NjcyNTc0ODcsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNzY1NDU3NDg3LCJmaXJzdE5hbWUiOiJNYXRoaWFzIiwibGFzdE5hbWUiOiJKZW5zZW4iLCJlbmFibGVkIjp0cnVlLCJwcml2YWN5UG9saWN5QWNjZXB0ZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiI3NzA2YWM1MC05ODVhLTExZjAtYTliNS03OTJlMjE5NGE1ZDQiLCJjdXN0b21lcklkIjoiMTM4MTQwMDAtMWRkMi0xMWIyLTgwODAtODA4MDgwODA4MDgwIn0.dIj_55gpHxlq8GGUuzgVBJYJojCMqIMZrUpdcPE2kBZ3NXWlMvXL3HwCDg4V6kRoPFaOvwr3Q3XnW7aN2EYA_w';          
  private deviceId  = '37767a50-985c-11f0-a9b5-792e2194a5d4';
  private securityDeviceId = 'f43094d0-d68e-11f0-869d-9726f60f35d2';

  constructor(private http: HttpClient) {}

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
      'speed',
      'temperature_c',
      'latitude',
      'longitude',
    ].join(',');

    const url = `${this.tbBaseUrl}/api/plugins/telemetry/DEVICE/${this.deviceId}/values/timeseries?keys=${keys}&limit=1`;
    const headers = new HttpHeaders({ 'X-Authorization': `Bearer ${this.jwtToken}` });
    return this.http.get(url, { headers });
  }

  getSecurityTelemetry(): Observable<any> {
    const keys = ['alarm', 'lock', 'lock_bool'].join(',');
    const url = `${this.tbBaseUrl}/api/plugins/telemetry/DEVICE/${this.securityDeviceId}/values/timeseries?keys=${keys}&limit=1`;
    const headers = new HttpHeaders({ 'X-Authorization': `Bearer ${this.jwtToken}` });
    return this.http.get(url, { headers });
  }

  sendTestTelemetryWithDeviceToken(deviceToken: string): Observable<any> {
    const url = `${this.tbBaseUrl}/api/v1/${deviceToken}/telemetry`;

    const body = {
      temperature: 25,
      humidity: 50
    };

    return this.http.post(url, body);
  }
}
