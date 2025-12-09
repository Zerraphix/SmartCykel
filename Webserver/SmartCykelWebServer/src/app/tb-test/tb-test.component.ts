import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ThingsboardTestService } from '../thingsboard-test.service';

@Component({
  selector: 'app-tb-test',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './tb-test.component.html',
  styleUrl: './tb-test.component.css'
})
export class TbTestComponent {

  restResult: any;
  restError: any;

  devicePostResult: any;
  devicePostError: any;

  deviceToken: string = ''; // for testing device access token POST

  loadingRest = false;
  loadingDevicePost = false;

  constructor(private tbService: ThingsboardTestService) {}

  testRestGet() {
    this.loadingRest = true;
    this.restResult = null;
    this.restError = null;

    this.tbService.getLatestTelemetry().subscribe({
      next: res => {
        this.restResult = res;
        this.loadingRest = false;
      },
      error: err => {
        this.restError = err;
        this.loadingRest = false;
      }
    });
  }

  testDevicePost() {
    this.loadingDevicePost = true;
    this.devicePostResult = null;
    this.devicePostError = null;

    if (!this.deviceToken) {
      this.devicePostError = 'Please enter a device access token.';
      this.loadingDevicePost = false;
      return;
    }

    this.tbService.sendTestTelemetryWithDeviceToken(this.deviceToken).subscribe({
      next: res => {
        this.devicePostResult = res;
        this.loadingDevicePost = false;
      },
      error: err => {
        this.devicePostError = err;
        this.loadingDevicePost = false;
      }
    });
  }
}