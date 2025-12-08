import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {path: '', loadComponent: () =>
  import('./home/home.component').then(it => it.HomeComponent)},
  {path: 'test', loadComponent: () =>
  import('./tb-test/tb-test.component').then(it => it.TbTestComponent)}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
