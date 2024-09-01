import { Controller, Get, OnModuleInit } from '@nestjs/common';
import { MessagePattern, Payload } from '@nestjs/microservices';

@Controller()
export class AppController {
  constructor(
  ) {}


  @Get("/")
  getHello(): string {
    return "Hello World!";
  }

  @MessagePattern('send-email')
  sendEmail(@Payload() data: any) {
    console.log("Received");
    console.log(data);
    return true;
  }
}
