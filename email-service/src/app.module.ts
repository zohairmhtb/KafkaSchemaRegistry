import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { AppController } from './app.controller';
// import { ClientsModule, Transport } from '@nestjs/microservices';
// import { CommandParserMiddleware } from './middleware/commandParser.middleware';

@Module({
  imports: [
  ],
  controllers: [AppController],
  providers: [],
})
export class AppModule {
}
