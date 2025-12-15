import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ThingsboardTestService } from '../thingsboard-test.service';

interface TbPoint {
  ts: number;
  value: any;
}

@Component({
  selector: 'app-homepage',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  isConnected = false;

  batteryLevel = 0;          
  batteryRemainingText = '';   
  batteryRemainingHours: number | null = null;
  batteryVoltage: number | null = null;
  batteryCurrent: number | null = null;
  batteryState = '';           
  batteryCharging = false;

  humidity: number | null = null;
  latitude: number | null = null;
  longitude: number | null = null;
  speedKph: number | null = null;
  temperatureC: number | null = null;

  alarmActive = false;
  isLocked = false;
  lockStateText = 'UNKNOWN';

  estimatedRangeKm: number | null = null;
  lastRideSummary = 'No ride data yet.';
  lastUpdate: Date | null = null;

  constructor(private tbService: ThingsboardTestService) {}

    ngOnInit(): void {
    this.refreshTelemetry();
    this.refreshSecurity();
  }

  refreshSecurity(): void {
    this.tbService.getSecurityTelemetry().subscribe({
      next: res => {
        const alarm = this.getLatest(res, 'alarm');
        const lock = this.getLatest(res, 'lock');
        const lockBool = this.getLatest(res, 'lock_bool');

        const toBool = (v: any) =>
          v === true || v === 'true' || v === 1 || v === '1';

        this.alarmActive = alarm ? toBool(alarm.value) : false;

        if (lockBool) {
          this.isLocked = toBool(lockBool.value);
        } else if (lock) {
          this.isLocked = String(lock.value).toUpperCase() === 'LOCKED';
        } else {
          this.isLocked = false;
        }

        this.lockStateText = lock ? String(lock.value) : (this.isLocked ? 'LOCKED' : 'UNLOCKED');
      },
      error: err => {
        console.error('Failed to load security telemetry', err);
      }
    });
  }


  private getLatest(raw: any, key: string): TbPoint | null {
    const arr = raw?.[key];
    if (Array.isArray(arr) && arr.length > 0) {
      return arr[arr.length - 1];
    }
    return null;
  }

    refreshTelemetry(): void {
    this.tbService.getLatestTelemetry().subscribe({
      next: res => {
        const socPoint = this.getLatest(res, 'battery_soc');
        this.isConnected = !!socPoint;

        this.batteryLevel = socPoint ? Number(socPoint.value) || 0 : 0;

        const remText = this.getLatest(res, 'battery_remaining_text');
        this.batteryRemainingText = remText ? String(remText.value) : '';

        const remH = this.getLatest(res, 'battery_remaining_hours');
        this.batteryRemainingHours = remH ? Number(remH.value) || null : null;

        const volt = this.getLatest(res, 'battery_voltage');
        this.batteryVoltage = volt ? Number(volt.value) || null : null;

        const cur = this.getLatest(res, 'battery_current');
        this.batteryCurrent = cur ? Number(cur.value) || null : null;

        const state = this.getLatest(res, 'battery_state');
        this.batteryState = state ? String(state.value) : '';

        const charging = this.getLatest(res, 'battery_charging');
        this.batteryCharging = charging
          ? charging.value === 'true' || charging.value === true
          : false;

        const speed = this.getLatest(res, 'speed');
        this.speedKph = speed ? Number(speed.value) || null : null;

        const temp = this.getLatest(res, 'temperature_c');
        this.temperatureC = temp ? Number(temp.value) || null : null;

        const hum = this.getLatest(res, 'humidity');
        this.humidity = hum ? Number(hum.value) || null : null;

        const lat = this.getLatest(res, 'latitude');
        this.latitude = lat ? Number(lat.value) || null : null;

        const lon = this.getLatest(res, 'longitude');
        this.longitude = lon ? Number(lon.value) || null : null;

        if (this.batteryRemainingHours != null) {
          this.estimatedRangeKm = Math.round(this.batteryRemainingHours * 15);
        } else {
          this.estimatedRangeKm = null;
        }

        const allPoints = [
          socPoint, remText, remH, volt, cur, hum, lat, lon, speed, temp
        ].filter(p => !!p) as TbPoint[];
        if (allPoints.length) {
          const maxTs = Math.max(...allPoints.map(p => p.ts));
          this.lastUpdate = new Date(maxTs);
        }

        this.lastRideSummary =
          this.speedKph != null && this.temperatureC != null
            ? `Speed: ${this.speedKph.toFixed(1)} km/h • Temp: ${this.temperatureC.toFixed(1)} °C • Battery ${this.batteryLevel}%.`
            : `Battery at ${this.batteryLevel}% – more ride data coming later.`;
      },
      error: err => {
        console.error('Failed to load telemetry', err);
        this.isConnected = false;
      }
    });
  }
}
