<?php

use Illuminate\Database\Seeder;

class UsersTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        App\User::create([
            'name' => 'David García', 
            'email' => 'ccristhiangarcia@gmail.com', 
            'password' => bcrypt('secret'), 
            'api_token' => str_random(60)
        ]);

        factory(App\User::class, 10)->create();
    }
}
