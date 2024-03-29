<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/
Route::group(['prefix' => 'v1/'], function () {
    Route::group(['middleware' => 'auth:api'], function () {
        Route::get('/ebill/{word}', function ($word) {
            return [
                'original' => $word, 
                'upper' => strtoupper($word)
            ];            
        });

        Route::get('/profile', function () {
            return Auth::guard('api')->user();
        });
    });
});
