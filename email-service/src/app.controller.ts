import { Controller, Get, OnModuleInit, UseInterceptors } from '@nestjs/common';
import { MessagePattern, Payload } from '@nestjs/microservices';
import { EmailCommand } from './commands/email.command';
import { SchemaRegistry } from '@kafkajs/confluent-schema-registry';

@Controller()
export class AppController {
  private schemaRegistry: SchemaRegistry;
  constructor(
  ) {
    this.schemaRegistry = new SchemaRegistry({host: `http://${process.env.SCHEMA_REGISTRY_HOST}:${process.env.SCHEMA_REGISTRY_PORT}`});
  }


  @Get("/")
  getHello(): string {
    return "Hello World!";
  }

  @MessagePattern('send-email')
  async sendEmail(@Payload() data: any) {
    const parsedData:EmailCommand = await this.schemaRegistry.decode(data);
    return true;
  }
}
